import * as _ from 'lodash';
import * as React from 'react';
import { Collapse } from 'react-bootstrap';

import * as codeRefActions from '../../actions/codeReference';
import * as actions from '../../actions/experiment';
import { getExperimentTensorboardUrl } from '../../constants/utils';
import CodeReference from '../../containers/codeReference';
import { ExperimentModel } from '../../models/experiment';
import { getExperimentCloning } from '../../utils/cloning';
import Description from '../description';
import { EmptyList } from '../empty/emptyList';
import MDEditor from '../mdEditor/mdEditor';
import CloningLinkMetaInfo from '../metaInfo/cloningLinkMetaInfo';
import JobCountMetaInfo from '../metaInfo/counts/jobCountMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import ResourcesMetaInfo from '../metaInfo/resourcesMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Name from '../name';
import Packages from '../packages';
import Refresh from '../refresh';
import RunEnv from '../runEnv';
import Status from '../status';
import VerticalTable from '../tables/verticalTable';
import Tags from '../tags';

export interface Props {
  experiment: ExperimentModel;
  onUpdate: (updateDict: { [key: string]: any }) => actions.ExperimentAction;
  onFetch: () => actions.ExperimentAction;
  onFetchCodeReference: () => codeRefActions.CodeReferenceAction;
}

export interface State {
  openMetrics: boolean;
  openDeclarations: boolean;
  openRunEnv: boolean;
  openPackages: boolean;
  openDataRefs: boolean;
  openCodeRef: boolean;
}

export default class ExperimentOverview extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      openMetrics: false,
      openDeclarations: false,
      openRunEnv: false,
      openPackages: false,
      openDataRefs: false,
      openCodeRef: false,
    };
  }

  public refresh = () => {
    this.props.onFetch();
  };

  public render() {
    const experiment = this.props.experiment;

    if (_.isNil(experiment)) {
      return EmptyList(false, 'experiment', 'experiment');
    }
    return (
      <div className="entity-details">
        <div className="row">
          <div className="col-md-12">
            <div className="row">
              <div className="col-md-11">
                <Description
                  description={experiment.description}
                  showEmpty={true}
                  onSave={(description: string) =>  { this.props.onUpdate({description}); }}
                />
              </div>
              <div className="col-md-1">
                <Refresh callback={this.refresh} pullRight={false}/>
              </div>
            </div>
            <div className="row">
              <div className="col-md-11">
                <Name
                  name="Experiment Name"
                  value={experiment.name || experiment.unique_name}
                  icon="fa-cube"
                  onSave={(name: string) =>  { this.props.onUpdate({name}); }}
                />
              </div>
            </div>
            <div className="meta">
              <UserMetaInfo user={experiment.user} inline={true}/>
              <DatesMetaInfo
                createdAt={experiment.created_at}
                updatedAt={experiment.updated_at}
                inline={true}
              />
              <JobCountMetaInfo count={experiment.num_jobs} inline={true}/>
              {experiment.original &&
              <CloningLinkMetaInfo
                cloning={getExperimentCloning(experiment.original, experiment.cloning_strategy)}
                inline={true}
              />
              }
            </div>
            <div className="meta">
              <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at} inline={true}/>
              <Status status={experiment.last_status}/>
            </div>
            <ResourcesMetaInfo resources={experiment.resources}/>
            {experiment.has_tensorboard &&
            <div className="meta">
              <span className="meta-info meta-dashboard">
                <i className="fa fa-link icon" aria-hidden="true"/>
                <a
                  href={getExperimentTensorboardUrl(experiment.project, experiment.id)}
                  className="title-link"
                >Tensorboard
                </a>
              </span>
            </div>
            }
            <Tags
              tags={experiment.tags}
              onSave={(tags: string[]) =>  { this.props.onUpdate({tags}); }}
            />
            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-declarations">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openDeclarations: !this.state.openDeclarations })}
                  >
                    <i className="fa fa-gear icon" aria-hidden="true"/>
                    <span className="title">Declarations:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openDeclarations}>
              <div className="row">
                <div className="col-md-12">
                  <VerticalTable values={experiment.declarations || {}}/>
                </div>
              </div>
            </Collapse>

            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-metrics">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openMetrics: !this.state.openMetrics })}
                  >
                    <i className="fa fa-area-chart icon" aria-hidden="true"/>
                    <span className="title">Metrics:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openMetrics}>
              <div className="row">
                <div className="col-md-12">
                  <VerticalTable values={experiment.last_metric || {}}/>
                </div>
              </div>
            </Collapse>

            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-data-refs">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openDataRefs: !this.state.openDataRefs })}
                  >
                    <i className="fa fa-database icon" aria-hidden="true"/>
                    <span className="title">Data refs:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openDataRefs}>
              <div className="row">
                <div className="col-md-12">
                  <VerticalTable values={experiment.data_refs || {}}/>
                </div>
              </div>
            </Collapse>

            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-run-env">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openRunEnv: !this.state.openRunEnv })}
                  >
                    <i className="fa fa-code icon" aria-hidden="true"/>
                    <span className="title">Run environment:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openRunEnv}>
            <div className="row">
              <div className="col-md-12">
                <RunEnv runEnv={experiment.run_env || {}}/>
              </div>
            </div>
            </Collapse>

            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-code-ref">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openCodeRef: !this.state.openCodeRef })}
                  >
                    <i className="fa fa-code-fork icon" aria-hidden="true"/>
                    <span className="title">Code reference:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openCodeRef}>
            <div className="row">
              <div className="col-md-12">
                <CodeReference fetchData={this.props.onFetchCodeReference} codeReferenceId={experiment.code_reference}/>
              </div>
            </div>
            </Collapse>

            <div className="row">
              <div className="col-md-12">
                <div className="meta meta-header meta-packages">
                  <span
                    className="meta-info"
                    onClick={() => this.setState({ openPackages: !this.state.openPackages })}
                  >
                    <i className="fa fa-file-archive-o icon" aria-hidden="true"/>
                    <span className="title">Packages:</span>
                  </span>
                </div>
              </div>
            </div>
            <Collapse in={this.state.openPackages}>
            <div className="row">
              <div className="col-md-12">
                <Packages runEnv={experiment.run_env || {}}/>
              </div>
            </div>
            </Collapse>

            <MDEditor
              content={experiment.readme}
              onSave={(readme: string) => { this.props.onUpdate({readme}); }}
            />
          </div>
        </div>
      </div>
    );
  }
}
