import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { getBuildUrl, getExperimentUrl, getGroupUrl, splitUniqueName } from '../../constants/utils';

import * as actions from '../../actions/experiment';
import { isDone } from '../../constants/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { ExperimentModel } from '../../models/experiment';
import { getBookmark } from '../../utils/bookmarks';
import { getExperimentCloning } from '../../utils/cloning';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import BuildLinkMetaInfo from '../metaInfo/buildLinkMetaInfo';
import CloningLinkMetaInfo from '../metaInfo/cloningLinkMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import GroupLinkMetaInfo from '../metaInfo/groupLinkMetaInfo';
import IdMetaInfo from '../metaInfo/idMetaInfo';
import TaskRunMetaInfo from '../metaInfo/taskRunMetaInfo';
import UserMetaInfo from '../metaInfo/userMetaInfo';
import Status from '../status';
import Tags from '../tags';
import ExperimentActions from './experimentActions';

export interface Props {
  experiment: ExperimentModel;
  metrics: string[];
  declarations: string[];
  onDelete: () => actions.ExperimentAction;
  onStop: () => actions.ExperimentAction;
  onArchive: () => actions.ExperimentAction;
  onRestore: () => actions.ExperimentAction;
  showBookmarks: boolean;
  bookmark: () => actions.ExperimentAction;
  unbookmark: () => actions.ExperimentAction;
  removeFromSelection?: () => void;
  useCheckbox: boolean;
  selectHandler: () => void;
  selected: boolean;
  reducedForm: boolean;
}

function Experiment({
                      experiment,
                      metrics,
                      declarations,
                      onDelete,
                      onStop,
                      onArchive,
                      onRestore,
                      bookmark,
                      unbookmark,
                      useCheckbox,
                      showBookmarks,
                      selectHandler,
                      selected,
                      reducedForm,
                      removeFromSelection,
                    }: Props) {
  const values = splitUniqueName(experiment.project);
  const bookmarkStar: BookmarkInterface = getBookmark(
    experiment.bookmarked, bookmark, unbookmark);
  let groupUrl = '';
  let groupValues: string[] = [];
  if (!_.isNil(experiment.experiment_group)) {
    groupValues = splitUniqueName(experiment.experiment_group);
    groupUrl = getGroupUrl(groupValues[0], groupValues[1], groupValues[2]);
  }
  let buildUrl = '';
  let buildValues: string[] = [];
  if (!_.isNil(experiment.build_job)) {
    buildValues = splitUniqueName(experiment.build_job);
    buildUrl = getBuildUrl(buildValues[0], buildValues[1], buildValues[3]);
  }
  const experimentActions = [];
  if (removeFromSelection) {
    experimentActions.push(
      {
        name: 'Remove from selection',
        icon: 'minus',
        callback: removeFromSelection
      }
    );
  }

  return (
    <tr className="list-item">
      {useCheckbox &&
      <td className="block">
        <input type="checkbox" checked={selected} onChange={selectHandler}/>
      </td>
      }
      <td className="block">
        <Status status={experiment.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getExperimentUrl(values[0], values[1], experiment.id)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experiment.name || experiment.unique_name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        {!reducedForm && <Description description={experiment.description}/>}
        {!reducedForm &&
        <div className="meta">
          <IdMetaInfo value={experiment.id} inline={true}/>
          <UserMetaInfo user={experiment.user} inline={true}/>
          <DatesMetaInfo
            createdAt={experiment.created_at}
            updatedAt={experiment.updated_at}
            inline={true}
          />
        </div>
        }
        {!reducedForm && <Tags tags={experiment.tags}/>}
      </td>
      <td className="block">
        <GroupLinkMetaInfo
          value={groupValues[2]}
          link={groupUrl}
        />
        <BuildLinkMetaInfo
          value={buildValues[3]}
          link={buildUrl}
        />
        {experiment.original &&
        <CloningLinkMetaInfo
          cloning={getExperimentCloning(experiment.original, experiment.cloning_strategy)}
        />
        }
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at}/>
      </td>
      {declarations.length > 0 && declarations.map((declaration: string, idx: number) =>
        <td className="block" key={idx}>
          {experiment.declarations ? JSON.stringify(experiment.declarations[declaration]) : ''}
        </td>)
      }
      {metrics.length > 0 && metrics.map((metric: string, idx: number) =>
        <td className="block" key={idx}>
          {experiment.last_metric ? experiment.last_metric[metric] : ''}
        </td>)
      }
      <td className="block pull-right">
        <ExperimentActions
          onDelete={onDelete}
          onStop={onStop}
          onArchive={experiment.deleted ? undefined : onArchive}
          onRestore={experiment.deleted ? onRestore : undefined}
          isRunning={!isDone(experiment.last_status)}
          pullRight={false}
          actions={experimentActions}
        />
      </td>
    </tr>
  );
}

export default Experiment;
