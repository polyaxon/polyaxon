import * as React from 'react';

import * as actions from '../actions/codeReference';
import { CodeReferenceModel } from '../models/codeReference';
import { EmptyList } from './empty/emptyList';
import VerticalTable from './tables/verticalTable';

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
          'git url': this.props.codeReference.git_url,
        };
        return (
          <div className="row">
            <div className="col-md-8">
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
