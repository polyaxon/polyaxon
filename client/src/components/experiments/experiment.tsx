import * as _ from 'lodash';
import * as React from 'react';
import { LinkContainer } from 'react-router-bootstrap';

import { getBuildUrl, getExperimentUrl, getGroupUrl, splitUniqueName } from '../../constants/utils';

import * as actions from '../../actions/experiment';
import { isDone } from '../../constants/statuses';
import { BookmarkInterface } from '../../interfaces/bookmarks';
import { ExperimentModel } from '../../models/experiment';
import { getBookmark } from '../../utils/bookmarks';
import BookmarkStar from '../bookmarkStar';
import Description from '../description';
import BuildLinkMetaInfo from '../metaInfo/buildLinkMetaInfo';
import DatesMetaInfo from '../metaInfo/datesMetaInfo';
import GroupLinkMetaInfo from '../metaInfo/groupLinkMetaInfo';
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
  showBookmarks: boolean;
  bookmark: () => actions.ExperimentAction;
  unbookmark: () => actions.ExperimentAction;
  reducedForm: boolean;
}

function Experiment({
                      experiment,
                      metrics,
                      declarations,
                      onDelete,
                      onStop,
                      bookmark,
                      unbookmark,
                      showBookmarks,
                      reducedForm
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
  return (
    <tr className="list-item">
      <td className="block">
        <Status status={experiment.last_status}/>
      </td>
      <td className="block">
        <LinkContainer to={getExperimentUrl(values[0], values[1], experiment.id)}>
          <a className="title">
            <i className="fa fa-cube icon" aria-hidden="true"/>
            {experiment.unique_name}
          </a>
        </LinkContainer>
        {showBookmarks &&
        <BookmarkStar active={bookmarkStar.active} callback={bookmarkStar.callback}/>
        }
        {!reducedForm && <Description description={experiment.description}/>}
        {!reducedForm &&
        <div className="meta">
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
      </td>
      <td className="block">
        <TaskRunMetaInfo startedAt={experiment.started_at} finishedAt={experiment.finished_at}/>
      </td>
      {declarations.length > 0 && declarations.map((declaration: string, idx: number) =>
        <td className="block" key={idx}>
          {experiment.declarations ? experiment.declarations[declaration] : ''}
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
          isRunning={!isDone(experiment.last_status)}
          pullRight={false}
        />
      </td>
    </tr>
  );
}

export default Experiment;
