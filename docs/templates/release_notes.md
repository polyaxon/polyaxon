## 0.2.5

This is a patch release on top of 0.2.3 containing no breaking changes.

 * Add `-l` option to `polyaxon run` to start log automatically after run command
 * Keep stream connection alive for logs (fix issue with ending sessions)
 
## 0.2.4

This is a patch release on top of 0.2.3 containing no breaking changes.

 * Update client auth: persist token after ephemeral login

## 0.2.3

 * Fix one major issue with events getting dropped, which led to experiments getting stuck in scheduled status.
 * Add out cluster tracking and instrumentation, users can now track experiment outside of Polyaxon and compare the experiments in Polyaxon.
 * Add possibility to create experiment and experiment groups without polyaxon specification, to allow users to run custom hyperparams tuning.
 * Add ttl and debug mode for runs.
 * Add customizable charts.
 * Add chart views saving functionality.
 * Add metrics views.
 * Extend query spec api to save metrics/params columns.
 * Add group metrics visualization and analysis [Beta].
 * Improve stability of experiment groups (some issues are still under investigation).
 * filter disabled nodes out from cluster api end points.
 * Add possibility to use GCE/S3/Azure as an outputs and artifact storage [Beta].
 * Update handling of internal tokens to increase job/experiment security and scoping.
 * Add traceback to the failure event status to get more context.
 * Add code reference endpoint for jobs and experiments.
 * Add data references tracking and extend experiment details api.
 * Add run environment tracking and extend experiment details api.
 * Add handling for evicted pods.
 * Init should not reinitialize ignore files and other cli config files.
 * Introduce ephemeral auth for experiment and jobs.
 * Update code reference to include branch, url, is_dirty.
 * Add possibility to merge-update tags and params/declarations.
 * Extract env var handling and typing.
 * Fix group stats (counts of experiments in different stages)
 * Fix a UI issue with flexbox in last chrome
 
## 0.2.2

This is a patch release on top of 0.2.0 containing only bug fixes and no breaking changes or features.

 * Fix issue with web hooks not serializing events correctly

## 0.2.1

This is a patch release on top of 0.2.0 containing only bug fixes and no breaking changes or features.

 * Fix issue with serializing experiment jobs' tolerations

## 0.2.0

 * Enhance filtering and sorting: better UI and dropdown with filter/sort options
 * Add saved queries
 * Experiments table dashboard can include optional columns: metrics and declarations/params. This will allow to compare experiments in one table.
 * Update log stream to show phase changes instead of disconnecting the session (now you can run and log without providing any id or checking the build)
 * Add REST API docs
 * Include bookmark indicator in dashboard lists
 * Refetch on tab changes to get latest updates
 * Remove some javascript dependencies and reduce bundle size
 * Add cli install to `install.polyaxon.com`
 * Add exception handling for actions, errors were preventing experiments/jobs from running
 * Lint helm chart
 * Add helm chart CI
 * Fix an issue with csrf token collection
 * Fix issue in reducer that made the state inconsistent
 * Fix an issue with dashboard pagination
 * Fix issue with bookmark page not loading experiments, and only loading when navigating tabs
 * Fix a bug that made loading experiments slow

## 0.1.9

 * Add config deployment app to help guide users through the configuration options when deploying Polyaxon
 * Add possibility to delete/stop jobs/experiments from dashboards
 * Update charts to support rolling updates
 * Optimize and fix some issues in some API endpoints
 * Optimize and reduce number of generated queries (More queries to optimize)
 * Update SDK to expose only one client
 * Add a delay before creating the experiment group's experiment to avoid not finding running status
 * Extend config manager to validate different generic specs and raise errors on bad config deployments
 * Abstract serialization of bookmarks to be used for lists
 * Fix an issue with the metrics api's pagination
 * Enhanced the filters ui
 * Consolidate installed libraries

## 0.1.8

  * Enable users to pull image from private registries
  * Add first version of an abstraction to seamlessly use cloud storage or persistent volumes for data, outputs, and logs
  * Annotate jobs with node used for the scheduling
  * Remove some optional env vars and move them to default values
  * Use configMap and secret envFrom to populate environment
  * Reduce number of partials
  * Update default page size to 20
  * Update usage of secrets and configs
  * Update clean commands
  * Fix an issue with check command
  * Fix a bug related to checking running experiment groups
  * Add missing tests for azure id creation
  * Enhance build and test process
  * Upgrade kubernetes client to 6.0.0
  * Upgrade web socket and request libs
  * Upgrade api and workers requirements
  * Update test requirements
  * Move label and pod/job states schemas to core

## 0.1.7

  * Add initial draft of actions
  * Add base integrations mechanism
  * Add notification via emai, slack, pagerduty, mattermost, discord, hipchat, webhooks ...
  * Enlarge docker's shm memory
  * Fix Microsoft authentication
  * Fix issue with cleaning pre-delete hooks
  * Remove deprecated polyaxon-lib
  * Separate email and admin user in helm chart
  * Fix api service with NodePort
  * Fix issue related to delete project command outside of initialized polyaxon workspace in CLI
  * Redirect directly to dashboard from CLI

## 0.1.6

  * Add possibility to deploy Polyaxon with tls.
  * Expose default toleration/affinity for builds, jobs, experiments.
  * Add affinity and toleration to spec environment.
  * Update spec to use node_selector instead of node_selectors.
  * Refactor worker/ps/default_worker/default_ps in environment section.
  * Update CLI init command to always create a new config for the project.
  * Add shortcuts -f for follow and -p for past for the logs commands.
  * Creating job/build/experiment/group with cli will cache the instance automatically for the following commands.
  * Fix some command suggestions.
  * Upgrade pyyaml, there was a security issue.
  * Improve docker build process.
  * Fix pytorch distributed example.
  * Update chart cleaning hook delete strategy.
  * Fix an issue with detecting the correct k8s minor version.
  * Fix issue with docker build process: image name should be lower case.
  * Fix Run meta info for builds, jobs, and groups on dashboard.
  * Add draft for stats and actions.

## 0.1.5

  * Build images: You can now pip install any file in your code folder without the need to call the file polyaxon_requirements.txt. Same thing if you need to build an image and have a shell script you just need to chmod +x the file and add it to the build setps.
  * Add bookmarking: You can bookmark your projects/groups/experiments/jobs/builds with Dashboard/API/CLI/Client. If your team is running too many hyper params tuning in many projects, finding the important experiments/jobs/builds can be exhausting since it requires searching each time. Bookmarks allow you to easily save important runs and have access to them in an easy way.
  * Add activity logs: shows recent create/update/delete activities in your team cluster or projects.
  * Add history/recently viewed: This is also something that some teams showed a lot of interests in having, using the platform for a couple of weeks/months and creating thousands of experiments per day, makes it very hard to access the right information.
  * Add support for external PostgreSQL: it's possible to link an external PostgreSQL database instead of the in-cluster one.
  * SSO: Add support for Microsoft Azure authentication. in addition to github, gitlab, bittbucket, and LDAP, now you can allow your team to signup/login to Polyaxon with Microsoft Azure authentication
  * Tooltips: for dates (creation date, update date, starting date, termination date) the dashboard shows a humanized version (e.g. X hours/days ago) this was not super helpful, and many users asked to have the possibility to see the exact values. On your dashboard you can see the dates values by hovering on any date and it will show datetime in the "YYYY-MM-DD HH: mm:ss" format.
  * Add docs for replication: the docs now has a section outlining different strategies for replicating Polyaxon.
  * Add docs for postgres HA strategies.
  * Add docs for Microsoft Azure authentication.

## 0.1.4

  * Fix some issues with node discovery
  * Optimize access to k8s api
  * Update image build process
  * Optimize resources monitoring on k8s
  * Add bookmarks for project, groups, experiments, jobs, builds
  * Fix some UI issues
  * Update docs
  * Other changes from 🇷🇺

## 0.1.3

  * Add support for outputs reference from other jobs and experiments by id and name
  * Update metrics tab with empty metrics
  * Add some error handling for spec validation
  * Fix the instruction pages

## 0.1.2

  * Update instructions tabs
  * Expose commit on the query spec
  * Add query spec docs
  * Add statuses tab
  * Add metrics tab
  * Add jobs cleaning
  * Update logic for allowing commits after delete notebooks
  * Update outputs logics for tensorboards

## 0.1.1

  * Update dockerizer process: moved from a worker based process that handles image builds to pod being scheduled to build the image if does not exists
  * Possibility to force rebuilding an image
  * Separate run into 2 sections: run and build
  * Add build specification
  * Add tensorboard and notebook specifications
  * Add generic job specification
  * Optimize services images and reduce their sizes
  * Upgrade docker client
  * upgrade kubernetes client
  * Add and test replication for api, workers, and monitors
  * Add tagging for projects, experiments, experiments groups, and jobs
  * Add possibility to name runs (experiments, groups, jobs, builds)
  * Add filtering, you can now filter based on our query spec: started_at:2015-01-01..2018-01-20, tags:foo|bar, metrics__loss:<=0.1
  * Add sorting, you can now sort by different attributes: -created_at, updated_at...
  * Remove upper limit on hptuning, this will allow hptuning algorithm worker to consume more cpu and converge faster.
  * Add download code: you can see now the commit made internally each time you upload the code
  * Add outputs download for experiments and jobs
  * Update tensorboards to support not only projects but also experiments and experiment group
  * Update and enhance ui
  * Add possibility to mount multiple data and outputs volumes
  * Extend the specification to allow to choose an output and data volumes to mount for an experiment or a job
  * Fix several usability and stability issues
  * Extend experiments api to allow to pull metrics and declarations

## 0.1.0

  * Add LDAP auth backend
  * Add identity abstraction for oauth and integrations
  * Add Github oauth
  * Add Bitbucket oauth
  * Add Gitlab oauth
  * Update landing page and dashboard design
  * Update signup/login pages
  * Update behaviour of experiment groups finished status
  * Expose more params for Bayesian optimization (algorithm was not converging sometime because of the default n_iter and n_warmup value)
  * Add more experiment group meta data: run dates and total time, iterations, status, and algorithm search
  * Fix issues with parsing numpy types in specification files

## 0.0.9

  * Optimize build process and handle concurrent build of the same repo: this will fix issues related to experiment getting stack in the build process and sometimes preventing the iterative hyperparameters algorithms from continuing the search.
  * Add advanced nodes scheduling for experiments and jobs: Previously users could set a default node selectors for core and experiments. Now they have the ability to override these selectors per experiment, experiment job for distributed runs, notebook, and tensorboard.
  * Fix upload command on Windows platform
  * Add more edge cases handling for resumed experiments
    * deleting original should delete resumed experiments
    * resuming a resumed experiment should resume the original experiment
  * Fix issue with stopping experiment groups
  * Add NFS provisioner, this is practical for testing the platform without the need to create a real NFS server.
  * Add event management and backbone for creating notifications and integrations
  * Add tracker
  * Add activity log
  * Update docs requirement

## 0.0.8

  * Add restart/resume/copy experiments
  * Fix issue with cyclic redirection when the user's session is expired.
  * Add platform logging
  * Update Bayesian optimization
  * Fix prospector for tests
  * Remove requirement for project name in specifications
  * Add google GKE tutorial

## 0.0.7

  * This new version has breaking changes:
  * Update specification
    * Add kind section to indicate the type of operation to run on Polyaxon.
    * Rename sequential search to grid search
    * Update early stopping schema to use optimization instead of higher: maximize | minimize
    * Move matrix to settings
    * Add config for search algorithms to settings
    * Remove run_type and export strategies form settings
    * All early_stop to stop both individual experiment from running or an experiment group or both.
    * Rename steps to build_steps in run section
    * Rename concurrent_experiment to concurrency
    * Add new method for sampling values
    * Possibilty to provide a seed
    * Rename Sequential search to grid search
  * Add new hyperparameters search algorithms:
    * Add hyperband
    * Add bayesian optimization [alpha]
  * Add continuous methods for sampling matrix params:
    * pvalues
    * uniform
    * quniform
    * loguniform
    * qloguniform
    * normal
    * qnormal
    * lognormal
    * qlognormal
  * Add first version of pipelines.
  * Show logs after experiment is finished [api, ui, client, cli].
  * Optimize plugin jobs [tensorboards and notebooks].
  * Separate dahsboard and runner.
  * Fixed bug issues.

## 0.0.6

 * Enhance single experiment spawner
 * Add MXNet spawner and support for distributed MXNet experiments
 * Add Pytorch spawner and support for distributed Pytorch experiments
 * Add Horovod spawner and support for distributed Horovod experiments [WIP]
 * Optimize Tensorflow spawner and distributed Tensorflow experiments
 * Optimize schedulers' logic
 * Optimize docker build process

## 0.0.5

 * Add early stopping and number of experiments
 * Use statuses for jupyter notebooks and tensorboards
 * Fix issue with starting multiple tensorboards
 * Rename deleted status to stopped
 * Add admin dashboard

## 0.0.4

 * Add Jupyter notebooks
 * Update Tensorboad deployments
 * Apply project permission to project plugin jobs, i.e. tensorboard and notebooks will only be accessible to users with enough project permissions
 * Update dashboard and ui
 * Fix some issues with kubernetes resources tracking

## 0.0.3

## 0.0.2

