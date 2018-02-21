import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Layout.css'
import globalStyles from '../../styles/style.scss'
import gridStyles from '../Grid/grid.css'
import {Header, Sidebar} from '../../components'
import cn from 'classnames'

class AppLayout extends React.Component {
  state = {
    spinnerCounter: 0,
  }

  componentDidMount() {
    this.timer = setInterval(() => {
      if (this.state.spinnerCounter === 3) {
        this.setState({
          spinnerCounter: 0
        })
      } else {
        this.setState({
          spinnerCounter: this.state.spinnerCounter + 1
        })
      }
    }, 2500)
  }

  componentWillUnmount() {
    clearInterval(this.timer)
  }

  render() {
    const {sidebarOpened, loading, title, children} = this.props
    const spinnerTexts = [
      'DeepMed is analyzing over 1 million records and treatments',
      'DeepMed is processing the most recent data available to analyze individual diagnoses',
      'DeepMed is covering actual data from hospitals and oncology clinics',
      'DeepMed covers data spanning nearly 30% of the country'
    ]
    // TODO spinner
    return (
      <div className={cn(s.container, sidebarOpened && s.sidebarOpened)}>
        <Header title={title}/>
        <Sidebar/>
        <div className={s.content}>
          {children}
        </div>
        {loading && (
          <div className='page-loader'>
            <div className='page-loader-sub-wrapper'>
              <div className='loader-spinner'>
                <div className='main'>
                  <div className='inside'/>
                </div>
              </div>
              <p className='push-top-3 text-lg'>{spinnerTexts[this.state.spinnerCounter]}</p>
            </div>
          </div>
        )}
      </div>
    )
  }
}


const mapState = state => ({
  loggedIn: state.user.loggedIn,
  sidebarOpened: state.global.sidebarOpened,
  loading: state.diagnosis.loading,
})

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(
  globalStyles,
  gridStyles,
  s,
)(AppLayout))
