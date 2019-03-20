import * as React from 'react';

import ReactMde from 'react-mde';

import * as Showdown from 'showdown';

import { getConverter, sanitizeHtml } from '../../utils/md';

import 'react-mde/lib/styles/css/react-mde-all.css';
import './md.less';

interface Props {
  content: string;
  handleChange: (content: string) => void;
}

export interface State {
  content: string;
  tab: 'write' | 'preview';
}

export default class MDEdit extends React.Component<Props, State> {
  public converter: Showdown.Converter;

  constructor(props: Props) {
    super(props);
    this.state = {
      content: this.props.content || '',
      tab: 'write'
    };
    this.converter = getConverter();
  }

  public handleValueChange = (content: string): void => {
    this.setState({content});
    this.props.handleChange(content);
  };

  public handleTabChange = (tab: 'write' | 'preview') => {
    this.setState({tab});
  };

  public render() {
    return (
      <ReactMde
        onChange={this.handleValueChange}
        onTabChange={this.handleTabChange}
        value={this.state.content}
        generateMarkdownPreview={(markdown: any) =>
          Promise.resolve(sanitizeHtml(this.converter.makeHtml(markdown)))
        }
        selectedTab={this.state.tab}
        minEditorHeight={200}
        maxEditorHeight={500}
        minPreviewHeight={200}
      />
    );
  }
}
