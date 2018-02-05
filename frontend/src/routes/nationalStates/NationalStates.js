import React from 'react'
import {connect} from 'react-redux'
import withStyles from 'isomorphic-style-loader/lib/withStyles'
import s from './NationalStates.scss'
// import {VectorMap} from 'react-jvectormap'
import {Line} from 'react-chartjs-2'

class NationalStates extends React.Component {
  render() {
    const {data} = this.props
    return (
      <div className="container container-full" data-children="same-height">

        <div className="row">
          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">

              <h2 className="no-margin text-center">Breast Cancer by State</h2>

              <div className="text-center">
                {/*{data.breast_cancer_by_state && (*/}
                  {/*<VectorMap*/}
                    {/*map="us_aea"*/}
                    {/*backgroundColor="transparent"*/}
                    {/*borderColor="#fb0000"*/}
                    {/*borderWidth={2}*/}
                    {/*series={data.breast_cancer_by_state}*/}
                    {/*containerStyle={{width: '100%', height: 400}}*/}
                  {/*/>*/}
                {/*)}*/}
              </div>

              <div className="row push-top-5">
                <div className="col-md-12 text-center">
                  <div
                    className="custom-panel custom-panel-condensed gray-bg inline-block  push-bot-0 text-left">
                    <p className="no-margin">Range:</p>
                    <div className="push-top-1">
                      <div className="display-table">
                        <div className="display-table-cell">
                          <div className="display-table-cell">
                            <span className="range-square" style={{backgroundColor: '#47cfd1'}}/>
                          </div>
                          <div className="display-table-cell">
                            <p className="no-margin line-height-100 small">&nbsp;106.6 to
                              118.3</p>
                          </div>
                        </div>
                        <div className="display-table-cell pad-left-1">
                          <div className="display-table-cell">
                            <span className="range-square" style={{backgroundColor: '#04a9a9'}}/>
                          </div>
                          <div className="display-table-cell">
                            <p className="no-margin line-height-100 small">&nbsp;118.7 to
                              125.5</p>
                          </div>
                        </div>
                        <div className="display-table-cell pad-left-1">
                          <div className="display-table-cell">
                            <span className="range-square" style={{backgroundColor: '#48ccf5'}}/>
                          </div>
                          <div className="display-table-cell">
                            <p className="no-margin line-height-100 small">&nbsp;125.9 to
                              132.0</p>
                          </div>
                        </div>
                        <div className="display-table-cell pad-left-1">
                          <div className="display-table-cell">
                            <span className="range-square" style={{backgroundColor: '#77c2d9'}}/>
                          </div>
                          <div className="display-table-cell">
                            <p className="no-margin line-height-100 small">&nbsp;132.3 to
                              144.9</p>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

            </div>
          </div>

          <div className="col-md-6">
            <div className="custom-panel custom-panel-condensed light-gray-bg" data-adjust="height">

              <h2 className="no-margin text-center">Breast Cancer at a Glance</h2>
              <div className="custom-panel custom-panel-condensed push-top-4">
                <div className="row row-condensed">
                  <div className="col-sm-12">
                    <p className="push-top-1 push-bot-2 text-center"><strong>Number per 100,000
                      females</strong></p>
                    {data.breast_cancer_at_a_glance && (
                      <Line
                        data={data.breast_cancer_at_a_glance}
                        width={500}
                        height={100}
                      />
                    )}
                  </div>
                </div>
                <div className="row row-condensed push-top-2">
                  <div className="col-sm-6">
                    <div className="custom-panel custom-panel-condensed no border green-bg push-bot-0">
                      <div className="display-table display-table-100">
                        <div className="display-table-cell">
                          <p className="no-margin text-white small">
                            Estimated New<br/>Cases in 2017
                          </p>
                        </div>
                        <div className="display-table-cell text-right">
                          <p className="no-margin text-white">
                            <strong>252,719</strong>
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="custom-panel custom-panel-condensed no border green-bg push-bot-0">
                      <div className="display-table display-table-100">
                        <div className="display-table-cell">
                          <p className="no-margin text-white small">
                            % of All New<br/>Cancer Cases
                          </p>
                        </div>
                        <div className="display-table-cell text-right">
                          <p className="no-margin text-white">
                            <strong>15.0%</strong>
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                  <div className="col-sm-6">
                    <div className="custom-panel custom-panel-condensed no border blue-bg push-bot-0">
                      <div className="display-table display-table-100">
                        <div className="display-table-cell">
                          <p className="no-margin text-white small">
                            Estimated<br/>Deaths in 2017
                          </p>
                        </div>
                        <div className="display-table-cell text-right">
                          <p className="no-margin text-white">
                            <strong>40,610</strong>
                          </p>
                        </div>
                      </div>
                    </div>
                    <div className="custom-panel custom-panel-condensed no border blue-bg push-bot-0">
                      <div className="display-table display-table-100">
                        <div className="display-table-cell">
                          <p className="no-margin text-white small">
                            % of All<br/>Cancer Deaths
                          </p>
                        </div>
                        <div className="display-table-cell text-right">
                          <p className="no-margin text-white">
                            <strong>6.8%</strong>
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div className="custom-panel custom-panel-condensed push-bot-0">
                <div className="display-table">
                  <div className="display-table-cell display-block-xs">
                    <div
                      className="custom-panel custom-panel-condensed gradient-bg text-center push-bot-0">
                      <p className="no-margin text-white"><strong>Percent<br/>Surviving 5</strong></p>
                      <p className="font-size-40 push-top-1 push-bot-1 text-white">
                        <strong>89.7%</strong></p>
                      <p className="no-margin text-white text-light">2017-2013</p>
                    </div>
                  </div>
                  <div className="display-table-cell display-block-xs push-top-2-xs pad-left-1">
                    <p className="push-bot-1">
                      Number of New Cases and Deaths per 100,00: The number of new cases of female
                      breast... <a href="#">Read more</a>
                    </p>
                    <p className="push-bot-1">
                      Lifetime Risk of Developing Cancer: Aproximately 12.4 percent of women will
                      be... <a href="#">Read more</a>
                    </p>
                    <p>
                      Prevalence of This Cancer: in 2014, there were an estimated 3,327,552
                      women... <a href="#">Read more</a>
                    </p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div className="row">
          <div className="col-sm-12">
            <div className="custom-panel custom-panel-condensed light-gray-bg">

              <h2 className="no-margin text-center">Breast Cancer by Age</h2>

              <div className="row push-top-4">
                <div className="col-md-6">
                  <div className="custom-panel custom-panel-condensed push-bot-0">
                    <p className="push-top-1 push-bot-2 text-center"><strong>Age-Specific Rates of
                      Breast Cancer in the United States</strong></p>
                    {data.breast_cancer_by_age && (
                      <Line
                        data={data.breast_cancer_by_age}
                        options={{
                          legend: {
                            display: false,
                            position: 'bottom'
                          }
                        }}
                        width={275}
                        height={100}
                      />
                    )}
                  </div>
                </div>
                <div className="col-md-6 push-top-1-sm">
                  <div className="custom-panel custom-panel-condensed push-bot-0">
                    <p className="push-top-1 push-bot-2 text-center"><strong>Percent of U.S. Women Who
                      Develop CancerAccording to o Their Age (2010-2012)</strong></p>
                    <div className="custom-panel custom-panel-condensed light-gray-bg push-bot-0">
                      <table className="table table-responsive table-middle-cell-align table-hover">
                        <thead>
                        <tr>
                          <th><h6>CURRENT AGE</h6></th>
                          <th><h6>10 YEARS</h6></th>
                          <th><h6>20 YEARS</h6></th>
                          <th><h6>30 YEARS</h6></th>
                        </tr>
                        </thead>
                        <tbody>
                        <tr>
                          <td><p className="no-margin">30</p></td>
                          <td><p className="no-margin">0.44</p></td>
                          <td><p className="no-margin">1.87</p></td>
                          <td><p className="no-margin">4.05</p></td>
                        </tr>
                        <tr>
                          <td><p className="no-margin">40</p></td>
                          <td><p className="no-margin">1.44</p></td>
                          <td><p className="no-margin">3.65</p></td>
                          <td><p className="no-margin">6.80</p></td>
                        </tr>
                        <tr>
                          <td><p className="no-margin">50</p></td>
                          <td><p className="no-margin">2.28</p></td>
                          <td><p className="no-margin">5.53</p></td>
                          <td><p className="no-margin">8.75</p></td>
                        </tr>
                        <tr>
                          <td><p className="no-margin">60</p></td>
                          <td><p className="no-margin">3.46</p></td>
                          <td><p className="no-margin">6.89</p></td>
                          <td><p className="no-margin">8.89</p></td>
                        </tr>
                        <tr>
                          <td><p className="no-margin">70</p></td>
                          <td><p className="no-margin">3.89</p></td>
                          <td><p className="no-margin">6.16</p></td>
                          <td><p className="no-margin">N/A</p></td>
                        </tr>

                        </tbody>
                      </table>
                    </div>
                  </div>
                </div>
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

export default connect(mapState, mapDispatch)(withStyles(s)(NationalStates))
