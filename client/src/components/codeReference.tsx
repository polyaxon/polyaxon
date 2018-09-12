import * as React from 'react';

import * as actions from '../actions/codeReference';
import { CodeReferenceModel } from '../models/codeReference';

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
        return (
          this.props.codeReference.id
        );
      }
      return (null);
    };
    return (
      <div>
        {getComponent()}
      </div>
    );
  }
}
