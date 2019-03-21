import * as React from 'react';

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

  public handleValueChange = (content: string): void => {
    this.setState({content});
    this.props.handleChange(content);
  };

  public render() {
    return (
      <textarea
        className="form-control input-sm"
        onChange={(event) => this.handleValueChange(event.target.value)}
      />
    );
  }
}
