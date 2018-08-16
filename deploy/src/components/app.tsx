import * as React from 'react';
import Footer from './footer';
import Header from './header';

function App() {
  return (
    <section id="root" className="hero is-fullheight">
      <Header/>
      <div className="hero-body layout">
        <div className="container">
          <div className="columns">
            <div className="column">
              <div className="tabs is-small">
                <ul>
                  <li className="is-active"><a>Setup</a></li>
                  <li><a>Configuration File</a></li>
                </ul>
              </div>
            </div>
          </div>
        </div>
      </div>
      <Footer/>
    </section>
  );
}

export default App;
