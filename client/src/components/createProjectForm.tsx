import * as React from 'react';
import { Button } from 'react-bootstrap';

export interface Props {
  handleSubmit: () => void;
}

const CreateProjectForm = ({handleSubmit}: any) => {

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label htmlFor="name">Project Name</label>
      </div>
      <div className="form-group">
        <label htmlFor="description">Project Description</label>
      </div>
      <Button bsStyle="default" type="submit">Submit</Button>
    </form>
  );
};

export default CreateProjectForm;
