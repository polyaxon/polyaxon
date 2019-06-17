import { Field, Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';

import * as actions from '../../../actions/options';
import { ErrorsField, getRequiredClass } from '../../../components/forms';
import SettingsSidebar from './sidebar';

export interface Props {
  isLoading: boolean;
  success: boolean;
  errors: any;
  onSave: (option: { [key: string]: any }) => actions.OptionAction;
}

export interface State {
  key: string;
  value: any;
}

export default class KeyOption extends React.Component<Props, State> {

  public onSave = (fValues: any) => {
    if (this.props.onSave) {
      const options: { [key: string]: any } = {};
      options[fValues.key] = fValues.value;
      this.props.onSave(options);
    }
  };

  public render() {

    const getForm = () => (
      <Formik
        initialValues={{}}
        onSubmit={(fValues: any, fActions: FormikActions<State>) => {
          this.onSave(fValues);
        }}
        render={(props: FormikProps<State>) => (
          <form onSubmit={props.handleSubmit}>
            <div className="row">
              <div className="col-sm-12">
                {ErrorsField(this.props.errors)}
                <label className={`control-label ${getRequiredClass(true)}`}>Key</label>
                <Field
                  name="key"
                  type="text"
                  className="form-control input-sm"
                />
                <label className="control-label">Value</label>
                <Field
                  name="value"
                  component="textarea"
                  type="text"
                  className="form-control input-sm"
                />
              </div>
            </div>
            <div className="row">
              <div className="col-md-2 name-buttons">
                <button type="submit" className="btn btn-sm btn-default" disabled={this.props.isLoading}>
                  Save
                </button>
              </div>
            </div>
          </form>
        )}
      />
    );
    return (
      <div className="row settings">
        <div className="col-md-3">
          <SettingsSidebar/>
        </div>
        <div className="col-md-9">
          <h3 className="menu-header">More options</h3>
          <span id="helpBlock" className="help-block">
            You can set any option by providing a valid key and value.
          </span>
          {getForm()}
        </div>
      </div>
    );
  }
}
