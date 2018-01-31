import React from 'react'
import Diagnosis from './Diagnosis'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'Diagnosis',
    component: <AppLayout><Diagnosis/></AppLayout>,
  }
}

export default action
