from io import StringIO
import os.path, logging, contextlib, glob
import curator
from .actionHistory import is_action_done, action_start, action_end

logging.basicConfig(format='%(asctime)s %(levelname)-9s %(message)s', level=logging.INFO)


def run_actions(elasticsearch_client, action_history_index_name, curator_config_file, action_files_path,
                override_running_state, dry_run):
    migration_scripts = sorted(map(os.path.basename, glob.glob(action_files_path + '/*.yaml')))

    for migration_script in migration_scripts:
        if is_action_done(elasticsearch_client, action_history_index_name, migration_script, override_running_state):
            logging.info('- Already executed [%s]' % (migration_script))
            continue
        if not dry_run:
            action_start(elasticsearch_client, action_history_index_name, migration_script)

        logging.info('- Executing [%s]' % (migration_script))
        f = StringIO()
        with contextlib.redirect_stdout(f):
            curator.run(curator_config_file, '%s/%s' % (action_files_path, migration_script), dry_run)

        if not dry_run:
            action_end(elasticsearch_client, action_history_index_name, migration_script, f.getvalue())
