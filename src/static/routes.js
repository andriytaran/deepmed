import React from 'react';
import { Route, Switch } from 'react-router';
import { HomeView, LoginView, DiagnosisView, NotFoundView } from './containers';
import requireAuthentication from './utils/requireAuthentication';

export default(
    <Switch>
        <Route exact path="/" component={requireAuthentication(HomeView)} />
        <Route path="/login" component={LoginView} />
        <Route path="/diagnosis" component={requireAuthentication(DiagnosisView)} />
        <Route path="*" component={NotFoundView} />
    </Switch>

);
