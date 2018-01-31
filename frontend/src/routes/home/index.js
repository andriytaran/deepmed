import React from 'react'
import Home from './Home'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'Home',
    component: <AppLayout><Home/></AppLayout>,
  }
}

export default action
