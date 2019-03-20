import * as React from 'react';

import * as Showdown from 'showdown';

import { getConverter } from '../../utils/md';
import MDEdit from './mdEdit';

import 'react-mde/lib/styles/css/react-mde-all.css';
import './md.less';

interface Props {
  content: string;
  onView: () => void;
  onSave: (content: string) => void;
}

export interface State {
  content: string;
}

export default class MDEditorEdit extends React.Component<Props, State> {
  public converter: Showdown.Converter;

  constructor(props: Props) {
    super(props);
    this.state = {
      content: this.props.content || '',
    };
    this.converter = getConverter();
  }

  public handleValueChange = (content: string): void => {
    this.setState({content});
  };

  public onSave = () => {
    this.props.onSave(this.state.content);
    this.props.onView();
  };

  public render() {
    return (
      <>
        <div className="row">
          <div className="col-md-12">
            <MDEdit
              content={this.state.content}
              handleChange={this.handleValueChange}
            />
          </div>
        </div>
        <div className="row">
          <div className="col-md-12 md-buttons">
            <button className="btn btn-sm btn-default" onClick={() => this.onSave()}>
              Save
            </button>
            <button className="btn btn-sm btn-default" onClick={() => this.props.onView()}>
              Cancel
            </button>
          </div>
        </div>
      </>
    );
  }
}
