import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './Home.css'
import {Row, Col, Link} from '../../components'
import {BC_FORM_ROUTE} from '../../routes'

class Home extends React.Component {
  render() {
    return (
      <div className={s.container}>
        <h1 className={s.header}>Please choose module</h1>
        <Row type='flex' justify='center' align='middle' gutter={16} className={s.modules}>
          <Col>
            <Link to={BC_FORM_ROUTE}>
              <div className={s.module}>
                Breast Cancer
              </div>
            </Link>
          </Col>
        </Row>
      </div>
    )
  }
}

const mapState = state => ({
})

const mapDispatch = {
}

export default connect(mapState, mapDispatch)(withStyles(s)(Home))
