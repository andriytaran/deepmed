import React from 'react'
import NationalStates from './NationalStates'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'National States',
    component: <AppLayout><NationalStates/></AppLayout>,
  }
}

export default action
