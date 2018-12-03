import * as _ from 'lodash';
import * as React from 'react';
import EntityMetaInfo from './metaInfo/entityMetaInfo';

import './name.less';

export interface Props {
  name: string;
  value: string;
  icon: string;
  onSave?: (name: string) => void;
}

export interface State {
  isEditMode: boolean;
  name: string;
}

export default class Description extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isEditMode: false,
      name: this.props.value || ''
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.value, prevProps.value)) {
      this.setState({
        ...prevState,
        name: this.props.value || ''
      });
    }
  }

  public handleInputChange = (name: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      name,
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
      this.props.onSave(this.state.name);
    }
    this.onView();
  };

  public render() {
    const getName = () => {
      return (
        <div className="name meta">
          <EntityMetaInfo
            name={this.props.name}
            value={this.props.value}
            icon={this.props.icon}
            inline={true}
          />
          {this.props.onSave && !this.state.isEditMode &&
          <span className="btn-link btn-link-margin" onClick={this.onEdit}>Edit</span>
          }
        </div>
      );
    };

    const getEditName = () => {
      return (
        <div className="row">
          <div className="col-md-10">
            <input
              type="text"
              className="form-control input-sm"
              value={this.state.name}
              onChange={(event) => this.handleInputChange(event.target.value)}
            />
            <span id="helpBlock" className="help-block">The name must be a slug and unique in this project.</span>
          </div>
          <div className="col-md-2 name-buttons">
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
            ? getEditName()
            : getName()
          }
        </div>
      </div>
    );
  }
}
