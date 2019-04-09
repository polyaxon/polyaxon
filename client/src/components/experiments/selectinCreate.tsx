import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { DescriptionField, DescriptionSchema } from '../forms/descriptionField';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';

export interface Props {
  onCreate: (form: { name: string, description: string }) => void;
  onClose: () => void;
  isLoading: boolean;
  errors: any;
  success: boolean;
}

export interface State {
  name: string;
  description: string;
}

const ValidationSchema = Yup.object().shape({
  name: NameSchema,
  description: DescriptionSchema,
});

export default class SelectionCreate extends React.Component<Props, {}> {

  public createSelection = (state: State) => {
    this.props.onCreate({
      name: state.name,
      description: state.description,
    });
  };

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.success) {
      this.props.onClose();
    }
  }

  public render() {
    return (
      <Formik
        initialValues={{name: '', description: ''}}
        validationSchema={ValidationSchema}
        onSubmit={(fValues: State, fActions: FormikActions<State>) => {
          this.createSelection(fValues);
        }}
        render={(props: FormikProps<State>) => (
          <form className="form-horizontal" onSubmit={props.handleSubmit}>
            {ErrorsField(this.props.errors)}
            {NameField(props, this.props.errors, false, '10')}
            {DescriptionField(props, this.props.errors, '10')}
            <div className="form-group">
              <div className="col-md-offset-2 col-md-10">
                <button
                  type="submit"
                  className="btn btn-success"
                  disabled={this.props.isLoading}
                >
                  Save
                </button>
              </div>
            </div>
          </form>
        )}
      />
    );
  }
}
