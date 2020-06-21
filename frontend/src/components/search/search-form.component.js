import React from 'react';
import 'date-fns';

import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Box from '@material-ui/core/Box';

import { KeyboardDatePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';

export default class SearchFormComponent extends React.Component {

    webPages = [
        'google.com',
        'bing.com'
    ];

    languages = [
        'Polish',
        'English'
    ];

    countries = [
        'Poland',
        'USA'
    ]

    render() {

        return (
            <form>
                <Box
                    boxShadow={3}
                    textAlign="left"
                    m={3}
                    p={2}
                >

                    <Typography variant="h5" gutterBottom >
                        Search
                    </Typography>

                    <MuiPickersUtilsProvider utils={DateFnsUtils}>
                        <Grid container justify="space-around">
                            <KeyboardDatePicker
                                disableToolbar
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                id="info-date-from"
                                label="Info date from"
                                onChange={(date, value) => { }}
                                KeyboardButtonProps={{
                                    'aria-label': 'change date',
                                }}
                            />

                            <KeyboardDatePicker
                                disableToolbar
                                variant="inline"
                                format="MM/dd/yyyy"
                                margin="normal"
                                id="info-date-to"
                                label="Info date to"
                                onChange={(date, value) => { }}
                                KeyboardButtonProps={{
                                    'aria-label': 'change date',
                                }}
                            />

                            <Autocomplete
                                id="web-page"
                                options={this.webPages}
                                style={{ width: 300 }}
                                openOnFocus
                                renderInput={(params) => <TextField {...params} label="Web page" margin="normal" />}
                            />

                            <Autocomplete
                                id="language"
                                options={this.languages}
                                style={{ width: 300 }}
                                openOnFocus
                                renderInput={(params) => <TextField {...params} label="Language" margin="normal" />}
                            />

                            <Autocomplete
                                id="country"
                                options={this.countries}
                                style={{ width: 300 }}
                                openOnFocus
                                renderInput={(params) => <TextField {...params} label="Country" margin="normal" />}
                            />

                            <TextField
                                id="any-phrase"
                                label="Any phrase"
                                margin="normal"
                            />

                        </Grid>
                    </MuiPickersUtilsProvider>

                    <Grid
                        style={{display: 'flex', justifyContent: 'flex-end'}}
                        justify="space-around"
                    >

                        <Button
                            variant="contained"
                            className="button-submit"
                            primary={true} 
                            style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                            Reset
                        </Button>

                        <Button
                            variant="contained"
                            className="button-submit"
                            color="primary"
                            primary={true}
                            style={{ position: 'relative', right: 5, top: 5, margin: 5 }} >
                            Search
                        </Button>
                    
                    </Grid>
                </Box>
            </form>
        );
    }
}