import { ErrorMessage, Field, Formik, FormikActions, FormikProps } from 'formik';
import * as jsYaml from 'js-yaml';
import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/options';
import { OptionModel } from '../../models/option';

import './option.less';

export interface Props {
  option: OptionModel;
  isLoading: boolean;
  errors: any;
  success: boolean;
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export interface State {
  value?: any;
  formValue?: any,
  isEditMode: boolean;
}

export default class Option extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      value: this.props.option.value,
      formValue: this.props.option.value,
      isEditMode: false
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    const newState = {...prevState};
    let updated = false;
    if (!_.isEqual(this.props.success, prevProps.success) && this.props.success) {
      newState.isEditMode = false;
      newState.value = this.parseValue(newState.formValue);
      updated = true;
    }
    if (!_.isEqual(this.props.option.value, prevProps.option.value)) {
      newState.value = this.props.option.value;
      updated = true;
    }
    if (updated) {
      this.setState({
        ...prevState,
        ...newState
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

  public handleInputChange = (value: string) => {
    this.setState((prevState, prevProps) => ({
      ...prevState,
      value,
    }));
  };

  public onSave = (fValues: any) => {
    if (this.props.onSave) {
      const options: { [key: string]: any } = {};
      if (this.isObj() && fValues) {
        options[this.props.option.key] =  jsYaml.safeLoad(fValues);
      } else {
        options[this.props.option.key] = fValues;
      }
      this.props.onSave(options);
    }
    this.setState((prevState, prevProps) => ({
      ...prevState,
      formValue: fValues
    }));
  };

  public isDict = () => {
    return this.props.option.typing === 'dict';
  };
  public isObj = () => {
    return ['int', 'float', 'str'].indexOf(this.props.option.typing) === -1 || this.props.option.is_list;
  };

  public parseValue = (value: any) => {
    if (this.isObj() && value) {
      try {
        return JSON.parse(value);
      } catch (e) {
        if (this.isDict()) {
          return jsYaml.safeLoad(value);
        }
      }
    }
    return value;
  };

  public getValue = (value: any) => {
    if (this.isObj() && value) {
      return JSON.stringify(value);
    }
    return value;
  };

  public render() {
    const isObj = this.isObj();

    const getForm = () => (
      <div className="row">
        <Formik
          initialValues={{option: this.getValue(this.state.value) || ''}}
          onSubmit={(fValues: any, fActions: FormikActions<State>) => {
            this.onSave(fValues.option);
          }}
          render={(props: FormikProps<State>) => (
            <form onSubmit={props.handleSubmit}>
              <div className={`${this.props.errors ? 'has-error' : ''}  col-sm-10`}>
                {this.props.option.typing === 'bool' &&
                <Field
                  name="option"
                  component="select"
                  className="form-control input-sm"
                >
                  <option value="true">True</option>
                  <option value="false">False</option>
                </Field>
                }
                {isObj && this.props.option.typing !== 'bool' &&
                <Field
                  name="option"
                  component="textarea"
                  type="text"
                  className="form-control input-sm"
                />
                }
                {!isObj && this.props.option.typing !== 'bool' &&
                <Field
                  name="option"
                  type="text"
                  className="form-control"
                />
                }
                {this.props.option.description &&
                <span id="helpBlock" className="help-block">{this.props.option.description}</span>
                }
                {this.props.errors && <div className="help-block">{this.props.errors}</div>}
                <ErrorMessage name="description">
                  {(errorMessage) => <div className="help-block">{errorMessage}</div>}
                </ErrorMessage>
              </div>
              <div className="col-md-2 name-buttons">
                <button type="submit" className="btn btn-sm btn-default" disabled={this.props.isLoading}>
                  Save
                </button>
                <button className="btn btn-sm btn-default" onClick={() => this.onView()}>
                  Cancel
                </button>
              </div>
            </form>
          )}
        />
      </div>
    );
    const getView = () => (
      <div className="col-md-7">
        {this.getValue(this.state.value)}
        {this.props.option.description &&
        <span id="helpBlock" className="help-block">
          <i className="fas fa-info-circle"/> info: {this.props.option.description}
        </span>
        }
      </div>
    );
    return (
      <div className="option">
        <div className="row">
          <div className="col-md-12">
            <label className="control-label">{this.props.option.key}</label> {
            !this.state.isEditMode &&
            <span className="btn-link btn-link-margin" onClick={this.onEdit}>
              <i className="fas fa-pen icon" aria-hidden="true"/>
            </span>
          }
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            {this.state.isEditMode ? getForm() : getView()}
          </div>
        </div>
      </div>
    );
  }
}
