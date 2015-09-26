import React from 'react'
import { Router, Route, Link, IndexRoute, IndexLink } from 'react-router'
import createBrowserHistory from '../../node_modules/react-router/node_modules/history/lib/createBrowserHistory'

var history = createBrowserHistory();

// components
var LoginForm = require('./components/LoginForm.jsx');
var RegisterForm = require('./components/RegisterForm.jsx');

var App = React.createClass({
    render: function () {
        return (
            <div>
                <div className="app">
                    {this.props.children}
                </div>
            </div>
        );
    }
});

var Home = React.createClass({
    render: function () {
        return (
            <div>
                Home
            </div>
        );
    }
});

var routes = (
    <Router>
        <Route path="/" component={App}>
            <IndexRoute component={Home}/>
            <Route path="login" component={LoginForm}/>
            <Route path="register" component={RegisterForm}/>
        </Route>
    </Router>
);

React.render(<Router history={history}>{routes}</Router>, document.body);

            // <Route path="login" component={LoginPage}/>
// var Parent = require('./components/Parent.jsx');

// React.render(<Parent />, document.getElementById('app'));