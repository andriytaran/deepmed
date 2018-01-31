import React from 'react'
import SpecificStates from './SpecificStates'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'Specific States',
    component: <AppLayout><SpecificStates/></AppLayout>,
  }
}

export default action
