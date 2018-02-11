import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Home.scss'
import DiagnosisForm from './DiagnosisForm'
import {getData} from '../../reducers/diagnosis'

class Home extends React.Component {
  handleSubmit = (e) => {
    e.preventDefault()
    this.form.validateFields((err, values) => {
      if (!err) {
        this.props.getData(values)
      }
    })
  }

  render() {
    return (
      <div className='container container-full text-center'>
        <div className='row'>
          <div className='col-md-12'>
            <div className='custom-panel custom-panel-md transparent-bg no-border push-bot-0'>
              <h2 className='no-margin'>
                Feel free to list your conditions and let us figure it out or use Advanced Search to input your
                diagnosis in detail.
              </h2>
            </div>
          </div>
        </div>
        <div className='row'>
          <div className='col-md-12'>
            <div className='custom-panel custom-panel-md light-gray-bg'>
              <DiagnosisForm
                ref={ref => {
                  this.form = ref
                }}
                onSubmit={this.handleSubmit}
              />
            </div>
          </div>
        </div>
      </div>
    )
  }
}

const mapState = state => ({
  ...state.diagnosis,
})

const mapDispatch = {
  getData,
}

export default connect(mapState, mapDispatch)(withStyles(s)(Home))
