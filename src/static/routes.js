import React from 'react';
import { Route, Switch } from 'react-router';
import { HomeView, LoginView, DiagnosisView, NationalStatesView, SpecificStatesView, SimilarDiagnosesView, ResourcesView, NotFoundView } from './containers';
import requireAuthentication from './utils/requireAuthentication';

export default(
    <Switch>
        <Route exact path="/" component={requireAuthentication(HomeView)} />
        <Route path="/login" component={LoginView} />
        <Route path="/diagnosis" component={requireAuthentication(DiagnosisView)} />
        <Route path="/national-states" component={requireAuthentication(NationalStatesView)} />
        <Route path="/specific-states" component={requireAuthentication(SpecificStatesView)} />
        <Route path="/similar-diagnoses" component={requireAuthentication(SimilarDiagnosesView)} />
        <Route path="/resources" component={requireAuthentication(ResourcesView)} />
        <Route path="*" component={NotFoundView} />
    </Switch>

);
