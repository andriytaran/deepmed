import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './SimilarDiagnoses.scss'
import {getAgeRangeLabel} from '../../utils'
import {Spin} from '../../components'
import isNil from 'lodash/isNil'

class SimilarDiagnoses extends React.Component {
  render() {
    const {similarDiagnoses} = this.props
    return (
      <div className="container container-full" data-children="same-height">
        <div className="row">
          <div className="col-md-12">
            <div className="custom-panel custom-panel-condensed push-bot-0">
              <div className="scroll-y scroll-x">
                <table className="table table-responsive table-middle-cell-align table-hover">
                  <thead>
                  <tr>
                    <th colSpan="4">
                      <h5 className="text-center">Diagnosis</h5>
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Status</h5>
                    </th>
                    <th colSpan="5">
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Treatment</h5>
                    </th>
                    <th colSpan="3">
                      <h5 className="text-center">Outcome</h5>
                    </th>
                  </tr>
                  <tr>
                    <th><h6 className="push-top-1">Age</h6></th>
                    <th><h6 className="push-top-1">Ethnicity</h6></th>
                    <th><h6 className="push-top-1">Size</h6></th>
                    <th><h6 className="push-top-1">Grade</h6></th>
                    <th><h6 className="push-top-1">ER</h6></th>
                    <th><h6 className="push-top-1">PR</h6></th>
                    <th><h6 className="push-top-1">HER2</h6></th>
                    <th><h6 className="push-top-1">Lat</h6></th>
                    <th><h6 className="push-top-1">Site</h6></th>
                    <th><h6 className="push-top-1">Type</h6></th>
                    <th><h6 className="push-top-1">+Nodes</h6></th>

                    <th><h6 className="push-top-1">Surgery</h6></th>
                    <th><h6 className="push-top-1">Chemo</h6></th>
                    <th><h6 className="push-top-1">Radiation</h6></th>
                    <th><h6 className="push-top-1">Year Dx</h6></th>
                    <th><h6 className="push-top-1">Survival Mos.</h6></th>
                    <th><h6 className="push-top-1">CoD</h6></th>
                  </tr>
                  </thead>
                  <tbody>
                  {similarDiagnoses.similar_diagnosis && similarDiagnoses.similar_diagnosis.map((item, i) =>
                    <tr key={i}>
                      <td><p className="no-margin">{item['Age']}</p></td>
                      <td><p className="no-margin">{item['Race_group']}</p></td>
                      <td><p className="no-margin">{item['Tumor_Size']}</p></td>
                      <td><p className="no-margin">{item['Grade']}</p></td>
                      <td><p className="no-margin">{item['ER_status']}</p></td>
                      <td><p className="no-margin">{item['PR_status']}</p></td>
                      <td><p className="no-margin">{item['HER2_Status']}</p></td>
                      <td><p className="no-margin">{item['Laterality']}</p></td>
                      <td><p className="no-margin">{item['Primary_site']}</p></td>
                      <td><p className="no-margin">{item['Type']}</p></td>
                      <td><p className="no-margin">{item['Nodes_Pos']}</p></td>
                      <td><p className="no-margin">{item['Surgery']}</p></td>
                      <td><p className="no-margin">{item['Chemo']}</p></td>
                      <td><p className="no-margin">{item['Radiation']}</p></td>
                      <td><p className="no-margin">{item['Year_dx']}</p></td>
                      <td><p className="no-margin">{item['Survival_months']}</p></td>
                      <td><p className="no-margin">{item['COD to site recode']}</p></td>
                    </tr>
                  )}
                  </tbody>
                </table>
                {isNil(similarDiagnoses.similar_diagnosis) && <Spin spinning/>}
              </div>
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

const mapDispatch = {}

export default connect(mapState, mapDispatch)(withStyles(s)(SimilarDiagnoses))
