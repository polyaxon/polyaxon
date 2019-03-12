import * as React from 'react';

import MDEdit from './mdEdit';
import MDView from './mdView';

import './md.less';

interface Props {
  content: string;
  onSave: (content: string) => void;
}

interface State {
  isEditMode: boolean;
}

export default class MDEditor extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isEditMode: false
    };
  }

  public onEdit = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        isEditMode: true,
      }
    }));
  };

  public onView = () => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      ...{
        isEditMode: false,
      }
    }));
  };

  public render() {
    return (
      <div className="row">
        <div className="col-md-12 mde">
          {this.state.isEditMode
            ? <MDEdit content={this.props.content} onView={this.onView} onSave={this.props.onSave}/>
            : <MDView content={this.props.content} onEdit={this.onEdit}/>
          }
        </div>
      </div>
    );
  }
}
