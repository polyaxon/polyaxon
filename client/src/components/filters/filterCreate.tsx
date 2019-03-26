import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { QueryField, QuerySchema } from './queryField';
import { SortField, SortSchema } from './sortField';

export interface Props {
  onCreate: (form: { name: string, query: string, sort: string }) => void;
  query: string;
  sort: string;
  isLoading: boolean;
  errors: any;
}

export interface State {
  name: string;
  query: string;
  sort: string;
}

const ValidationSchema = Yup.object().shape({
  name: NameSchema,
  query: QuerySchema,
  sort: SortSchema,
});

export default class FilterCreate extends React.Component<Props, {}> {

  public createSearch = (state: State) => {
    this.props.onCreate({
      name: state.name,
      query: state.query,
      sort: state.sort,
    });
  };

  public render() {
    const initialValues = {name: '', query: this.props.query, sort: this.props.sort};
    return (
      <Formik
        initialValues={initialValues}
        validationSchema={ValidationSchema}
        onSubmit={(fValues: State, fActions: FormikActions<State>) => {
          this.createSearch(fValues);
        }}
        render={(props: FormikProps<State>) => (
          <form className="form-horizontal" onSubmit={props.handleSubmit}>
            {ErrorsField(this.props.errors)}
            {NameField(props, this.props.errors, '10')}
            {QueryField(props, this.props.errors)}
            {SortField(props, this.props.errors)}
            <div className="form-group form-actions">
              <div className="col-sm-offset-2 col-sm-10">
                <button
                  type="submit"
                  className="btn btn-default btn-success"
                  disabled={this.props.isLoading}
                >
                  Save search
                </button>
              </div>
            </div>
          </form>
        )}
      />
    );
  }
}
