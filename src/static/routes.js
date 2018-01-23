import React from 'react';
import { Route, Switch } from 'react-router';
import { HomeView, LoginView, ProtectedView, NotFoundView } from './containers';
import requireAuthentication from './utils/requireAuthentication';

export default(
    <Switch>
        <Route exact path="/" component={requireAuthentication(HomeView)} />
        <Route path="/login" component={LoginView} />
        <Route path="/protected" component={requireAuthentication(ProtectedView)} />
        <Route path="*" component={NotFoundView} />
    </Switch>

);
