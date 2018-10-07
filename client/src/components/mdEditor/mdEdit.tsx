import * as React from 'react';

import ReactMde from 'react-mde';

import * as Showdown from 'showdown';

import { getConverter, sanitizeHtml } from '../../utils/md';

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

export default class MDEdit extends React.Component<Props, State> {
  public converter: Showdown.Converter;

  constructor(props: Props) {
    super(props);
    this.state = {
      content: this.props.content
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
      <div className="row">
        <div className="col-md-12">
          <div className="row">
            <div className="col-md-12">
              <ReactMde
                onChange={this.handleValueChange}
                value={this.state.content}
                generateMarkdownPreview={(markdown) =>
                  Promise.resolve(sanitizeHtml(this.converter.makeHtml(markdown)))
                }
                buttonContentOptions={{
                  iconProvider: (name: string) => <i className={`fa fa-${name}`}/>,
                }}
                minEditorHeight={300}
                maxEditorHeight={500}
                minPreviewHeight={500}
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
        </div>
      </div>
    );
  }
}
