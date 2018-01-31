import React from 'react'
import Resources from './Resources'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'Resources',
    component: <AppLayout><Resources/></AppLayout>,
  }
}

export default action
