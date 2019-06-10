import { Field, Formik, FormikActions, FormikProps } from 'formik';
import * as _ from 'lodash';
import * as React from 'react';

import * as actions from '../../actions/options';
import { OptionModel } from '../../models/option';

export interface Props {
  option: OptionModel;
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export interface State {
  value?: any;
  isEditMode: boolean;
}

export default class Option extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = {
      value: this.props.option.value,
      isEditMode: false
    };
  }

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (!_.isEqual(this.props.option.value, prevProps.option.value)) {
      this.setState({
        ...prevState,
        value: this.props.option.value,
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
      options[this.props.option.key] = fValues;
      this.props.onSave(options);
    }
    this.setState((prevState, prevProps) => ({
      ...prevState,
      value: this.isObj() ? JSON.parse(fValues) : fValues,
    }));
    this.onView();
  };

  public isObj = () => ['int', 'float', 'str'].indexOf(this.props.option.typing) === -1;

  public render() {

    const isObj = this.isObj();
    const getForm = () => (
      <div className="row">
        <Formik
          initialValues={{option: isObj ? JSON.stringify(this.state.value) : this.state.value}}
          onSubmit={(fValues: any, fActions: FormikActions<State>) => {
            this.onSave(fValues.option);
          }}
          render={(props: FormikProps<State>) => (
            <form onSubmit={props.handleSubmit}>
              <div className="col-sm-10">
                {isObj
                  ? <Field
                    name="option"
                    component="textarea"
                    type="text"
                    className="form-control input-sm"
                  /> : <Field
                    name="option"
                    type="text"
                    className="form-control"
                  />
                }
                {this.props.option.description &&
                <span id="helpBlock" className="help-block">{this.props.option.description}</span>
                }
              </div>
              <div className="col-md-2 name-buttons">
                <button type="submit" className="btn btn-sm btn-default">
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
        {isObj ? JSON.stringify(this.state.value) : this.state.value}
        {this.props.option.description &&
        <span id="helpBlock" className="help-block">{this.props.option.description}</span>
        }
      </div>
    );
    return (
      <>
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
      </>
    );
  }
}
