import React from 'react';
import ReactDOM from 'react-dom';
import './index.css';
import App from './App';
import Auth from'./components/auth'
import { Route, BrowserRouter } from 'react-router-dom';
import { CookiesProvider } from 'react-cookie';


function Router(){
  
    return (
    <React.StrictMode>
      <CookiesProvider>
        <BrowserRouter>
            <Route exact path="/" component={Auth} />
            <Route exact path="/movies" component={App} />
        </BrowserRouter>
      </CookiesProvider>
    </React.StrictMode>
    )   
}


ReactDOM.render(<Router />, document.getElementById('root'));


