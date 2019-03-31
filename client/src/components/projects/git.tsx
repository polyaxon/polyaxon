import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';

import { ErrorsField } from '../forms/errorsField';
import { UrlField, UrlSchema } from './forms/urlField';
import { VisibilityField } from './forms/visibilityField';

export interface Props {
  onSave?: (url: string, is_public: boolean) => void;
  isLoading: boolean;
  errors: any;
}

export interface State {
  url: string;
  visibility: string;
}

const EmptyState = {
  url: '',
  visibility: 'Public',
};

const ValidationSchema = Yup.object().shape({
  url: UrlSchema.required('Required'),
});

export default class GitUrl extends React.Component<Props, {}> {

  public onSave = (state: State) => {
    if (this.props.onSave) {
      this.props.onSave(state.url, state.visibility === 'Public');
    }
  };

  public render() {

    return (
      <div className="row">
        <div className="col-md-12">
          <Formik
            initialValues={EmptyState}
            validationSchema={ValidationSchema}
            onSubmit={(fValues: State, fActions: FormikActions<State>) => {
              this.onSave(fValues);
            }}
            render={(props: FormikProps<State>) => (
              <form className="form-inline" onSubmit={props.handleSubmit}>
                {ErrorsField(this.props.errors, 'col-sm-12')}
                {UrlField(props, this.props.errors)}
                {VisibilityField}
                <button
                  type="submit"
                  className="btn btn-default btn-sm"
                  disabled={this.props.isLoading}
                  placeholder="Git Url"
                >
                  Set git repo
                </button>
              </form>
            )}
          />
        </div>
      </div>
    );
  }
}
