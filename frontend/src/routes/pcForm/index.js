import React from 'react'
import PcForm from './PcForm'
import {AppLayout} from '../../components'
import {setCurrentRouteName} from '../../reducers/global'

async function action({store, route}) {
  store.dispatch(setCurrentRouteName(route.name))

  return {
    title: 'DeepMed',
    component: <AppLayout><PcForm/></AppLayout>,
  }
}

export default action
