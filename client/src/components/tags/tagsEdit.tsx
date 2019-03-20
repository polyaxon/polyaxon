import * as _ from 'lodash';
import * as React from 'react';

import CreatableSelect from 'react-select/lib/Creatable';

import './tags.less';

export interface Props {
  tags: string[];
  handleChange: (value: Array<{ label: string, value: string }>) => void;
}

export interface State {
  inputValue: string;
  value: Array<{ label: string, value: string }>;
}

export default class TagsEdit extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
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

  public handleChange = (value: any, actionMeta: any) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      value,
    }));
    this.props.handleChange(value);
  };

  public handleInputChange = (inputValue: string, actionMeta: any) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      inputValue,
    }));
  };

  public handleKeyDown = (event: any) => {
    const {inputValue, value} = this.state;
    if (!inputValue) {
      return;
    }
    switch (event.key) {
      case 'Enter':
      case 'Tab':
        const state = {inputValue: '', value};
        if (value.filter((v) => v.label === inputValue).length === 0) {
          state.value = [...value, {
            label: inputValue,
            value: inputValue,
          }];
          this.props.handleChange(state.value);
        }
        this.setState((prevState, prevProps) => ({
          ...prevState,
          ...state,
        }));
        event.preventDefault();
        break;
      default:
        break;
    }
  };

  public render() {
    const customStyles = {
      control: (base: any, state: any) => ({
        ...base,
        'boxShadow': state.isFocused ? 'inset 0 1px 1px rgba(0,0,0,.075), 0 0 8px rgba(102,175,233,.6)' : 0,
        'borderColor': state.isFocused
          ? '#66afe9'
          : base.borderColor,
        '&:hover': {
          borderColor: state.isFocused
            ? '#66afe9'
            : base.borderColor,
        }
      })
    };

    return (
      <div className="row">
        <div className="col-md-12">
          <CreatableSelect
            components={{
              DropdownIndicator: null
            }}
            className="input-multi-select"
            inputValue={this.state.inputValue}
            isClearable={true}
            isMulti={true}
            menuIsOpen={false}
            onChange={this.handleChange}
            onInputChange={this.handleInputChange}
            onKeyDown={this.handleKeyDown}
            value={this.state.value}
            styles={customStyles}
            theme={(theme) => ({
              ...theme,
              colors: {
                ...theme.colors,
                primary: '#66afe9',
              },
            })}
            placeholder=""
          />
        </div>
      </div>
    );
  }
}
