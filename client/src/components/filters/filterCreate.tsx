import { Formik, FormikActions, FormikProps } from 'formik';
import * as React from 'react';
import * as Yup from 'yup';
import { ErrorsField } from '../forms/errorsField';
import { NameField, NameSchema } from '../forms/nameField';
import { QueryField, QuerySchema } from './queryField';
import { SortField, SortSchema } from './sortField';

export interface Props {
  onCreate: (form: { name: string, query: string, sort: string }) => void;
  onClose: () => void;
  name: string;
  query: string;
  sort: string;
  isLoading: boolean;
  errors: any;
  success: boolean;
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

  public componentDidUpdate(prevProps: Props, prevState: State) {
    if (this.props.success) {
      this.props.onClose();
    }
  }

  public render() {
    const initialValues = {name: this.props.name, query: this.props.query, sort: this.props.sort};
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
            {NameField(props, this.props.errors, false,  '10')}
            {QueryField(props, this.props.errors)}
            {SortField(props, this.props.errors)}
            <div className="form-group">
              <div className="col-md-offset-2 col-md-10">
                <button
                  type="submit"
                  className="btn btn-success"
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
