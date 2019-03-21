import * as React from 'react';
import AceEditor from 'react-ace';

import 'brace/mode/yaml';
import 'brace/theme/github';

interface Props {
  content: string;
  handleChange: (content: string) => void;
}

export interface State {
  content: string;
}

export default class Polyaxonfile extends React.Component<Props, State> {

  constructor(props: Props) {
    super(props);
    this.state = {
      content: this.props.content || '',
    };
  }

  public shouldComponentUpdate(nextProps: Props, nextState: State) {
    return this.state.content === nextState.content;
  }

  public handleValueChange = (content: string): void => {
    this.setState({content});
    this.props.handleChange(content);
  };

  public render() {
    return (
      <AceEditor
        className="form-control input-sm"
        mode="yaml"
        theme="github"
        onChange={this.handleValueChange}
        name="UNIQUE_ID_OF_DIV"
        value={this.state.content}
        width="auto"
        editorProps={{$blockScrolling: true}}
      />
    );
  }
}
