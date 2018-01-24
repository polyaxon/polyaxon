import * as React from "react";


export interface Props {
  token: string;
}

function Token(probs: Props) {

  return (
    <div className="jumbotron jumbotron-action">
      Your token is: {probs.token}
    </div>
  );
};


export default Token;
