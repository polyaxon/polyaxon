import * as _ from 'lodash';
import * as React from 'react';

import { isTrue } from '../../constants/utils';
import TagsEdit from './tagsEdit';

import './tags.less';

export interface Props {
  tags: string[];
  onSave?: (tags: string[]) => void;
  isEditMode?: boolean;
}

export interface State {
  isEditMode: boolean;
  inputValue: string;
  value: Array<{ label: string, value: string }>;
}

export default class Tags extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      isEditMode: isTrue(props.isEditMode),
      inputValue: '',
      value: this.props.tags ? this.props.tags.map((tag) => ({label: tag, value: tag})) : [],
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.tags, prevProps.tags)) {
      this.setState({
        ...prevState,
        value: this.props.tags ? this.props.tags.map((tag) => ({label: tag, value: tag})) : [],
      });
    }
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

  public onSave = () => {
    if (this.props.onSave) {
      this.props.onSave(this.state.value.map((v) => v.value));
    }
    this.onView();
  };

  public handleChange = (value: Array<{ label: string, value: string }>) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      value,
    }));
  };

  public render() {
    const tags = this.props.tags;

    const getTags = () => {
      if (tags || this.props.onSave) {
        return (
          <div className="tags">
            {tags && !this.state.isEditMode && tags.map(
              (tag, idx) =>
                <span key={idx} className="label label-tags">
              <i className="fas fa-tags icon" aria-hidden="true"/> {tag}
            </span>
            )}
            {this.state.isEditMode &&
            <div className="row">
              <div className="col-md-10">
                <TagsEdit tags={tags} handleChange={this.handleChange}/>
              </div>
              <div className="col-md-2 tags-buttons">
                <button className="btn btn-sm btn-default" onClick={() => this.onSave()}>
                  Save
                </button>
                <button className="btn btn-sm btn-default" onClick={() => this.onView()}>
                  Cancel
                </button>
              </div>
            </div>

            }
            {this.props.onSave && !this.state.isEditMode &&
            <span className="btn-link" onClick={this.onEdit}>Update tags</span>
            }
          </div>
        );
      }
      return (null);
    };

    return (
      <div className="row">
        <div className="col-md-12">
          {getTags()}
        </div>
      </div>
    );
  }
}
