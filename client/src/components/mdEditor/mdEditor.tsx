import * as React from 'react';

import { isTrue } from '../../constants/utils';
import MDEditorEdit from './mdEditorEdit';
import MDEditorView from './mdEditorView';

import './md.less';

interface Props {
  content: string;
  onSave: (content: string) => void;
  isEditMode?: boolean;
}

interface State {
  isEditMode: boolean;
}

export default class MDEditor extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isEditMode: isTrue(this.props.isEditMode)
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
            ? <MDEditorEdit content={this.props.content} onView={this.onView} onSave={this.props.onSave}/>
            : <MDEditorView content={this.props.content} onEdit={this.onEdit}/>
          }
        </div>
      </div>
    );
  }
}
