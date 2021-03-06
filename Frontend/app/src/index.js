import React from 'react';
import ReactDOM from 'react-dom';
import './styles/index.css';
import App from './App';
import registerServiceWorker from './registerServiceWorker';
import CourseListView from './Components/CourseListView';
import Callback from './Components/Callback';
import { Router, Route,Switch } from 'react-router';
import { BrowserRouter } from 'react-router-dom'
import Auth from './utils/AuthService';
import history from './history';
import Profile from './Components/Profile';
import Courses from './Components/Courses';

const auth = new Auth();

const handleAuthentication = (nextState, replace) => {
  if (/access_token|id_token|error/.test(nextState.location.hash)) {
    auth.handleAuthentication();
  }
}
const Root = () => {
  return (
   <Router history={history} component={App}>
     <Switch>
        <Route exact path="/" render={(props) => <App auth={auth} {...props} />}/>
        <Route exact path="/listcourse" render={(props) => <Courses auth={auth} {...props} />}/>
        <Route path="/courses" render={(props) => <CourseListView auth={auth} {...props} />}/>
        <Route path="/callback" render={(props) => {
          handleAuthentication(props);
          return <Callback {...props} />
        }}/>
      <Route path="/profile" render={(props) => <Profile auth={auth} {...props} />} onEnter={() => auth.requireAuth()}/>
     </Switch>
    </Router>
  )
}

ReactDOM.render(<Root />, document.getElementById('root'));
registerServiceWorker();