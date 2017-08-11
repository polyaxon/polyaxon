import * as React from "react";
import {Field, reduxForm} from "redux-form";
import {Button} from "react-bootstrap";


export interface Props {
  handleSubmit: () => void;
}


const CreateProjectForm = ({handleSubmit}: any) => {

    return (
      <form onSubmit={handleSubmit}>
        <div className="form-group">
          <label htmlFor="name">Project Name</label>
          <Field name="name" component="input" type="text" className="form-control" />
        </div>
        <div className="form-group">
          <label htmlFor="description">Project Description</label>
          <Field name="description" component="input" type="text" className="form-control" />
        </div>
        <Button bsStyle="default" type="submit">Submit</Button>
      </form>
    )
};

export default reduxForm({
  form: 'CreateProjectForm'
})(CreateProjectForm);

