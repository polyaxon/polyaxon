import * as React from 'react';

import * as actions from '../actions/codeReference';
import { CodeReferenceModel } from '../models/codeReference';
import { EmptyList } from './empty/emptyList';
import VerticalTable from './verticalTable';

export interface Props {
  codeReference: CodeReferenceModel;
  fetchData: () => actions.CodeReferenceAction;
}

export default class CodeReference extends React.Component<Props, {}> {
  public componentDidMount() {
    this.props.fetchData();
  }

  public render() {
    const getComponent = () => {
      if (this.props.codeReference) {
        const values = {
          'commit': this.props.codeReference.commit,
          'branch': this.props.codeReference.branch,
          'head': this.props.codeReference.head,
          'is dirty': this.props.codeReference.is_dirty,
          'git url': this.props.codeReference.git_url,
          'repo': this.props.codeReference.repo
        };
        return (
          <div className="row">
            <div className="col-md-12">
              <VerticalTable values={values}/>
            </div>
          </div>
        );
      }
      return (
        <div className="row">
          <div className="col-md-12">
            {EmptyList(false, 'code reference', '')}
          </div>
        </div>
      );
    };
    return (
      <div className="row">
        <div className="col-md-12">
          {getComponent()}
        </div>
      </div>
    );
  }
}
