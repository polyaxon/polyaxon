import * as _ from 'lodash';
import * as React from 'react';

import './description.less';

export interface Props {
  description?: string;
  showEmpty?: boolean;
  onSave?: (description: string) => void;
}

export interface State {
  isEditMode: boolean;
  description: string;
}

export default class Description extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isEditMode: false,
      description: this.props.description || ''
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.description, prevProps.description)) {
      this.setState({
        ...prevState,
        description: this.props.description || ''
      });
    }
  }

  public handleInputChange = (description: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      description,
    }));
  };

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

  public onSave = () => {
    if (this.props.onSave) {
      this.props.onSave(this.state.description);
    }
    this.onView();
  };

  public render() {
    const getDescription = () => {
      let description = null;
      if (this.props.description) {
        description = this.props.description;
      } else if (this.props.showEmpty) {
        description = 'No description!';
      }
      return (
        <div className="description">
          {description}
          {this.props.onSave && !this.state.isEditMode &&
          <span className="btn-link btn-link-margin" onClick={this.onEdit}>Edit</span>
          }
        </div>
      );
    };

    const getEditDescription = () => {
      return (
        <div className="row">
          <div className="col-md-10">
            <input
              type="text"
              className="form-control input-sm"
              value={this.state.description}
              onChange={(event) => this.handleInputChange(event.target.value)}
            />
          </div>
          <div className="col-md-2 description-buttons">
            <button type="submit" className="btn btn-sm btn-default" onClick={() => this.onSave()}>
              Save
            </button>
            <button className="btn btn-sm btn-default" onClick={() => this.onView()}>
              Cancel
            </button>
          </div>
        </div>
      );
    };

    return (
      <div className="row">
        <div className="col-md-12">
          {this.state.isEditMode
            ? getEditDescription()
            : getDescription()
          }
        </div>
      </div>
    );
  }
}
