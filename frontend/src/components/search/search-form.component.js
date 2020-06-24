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

export default function SearchFormComponent() {

    const webPages = [
        'google.com',
        'bing.com'
    ];

    const languages = [
        'Polish',
        'English'
    ];

    const countries = [
        'Poland',
        'USA'
    ]

    const aWeekAgo = new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000)

    const [selectedDateFrom, setSelectedDateFrom] = React.useState(aWeekAgo);
    const handleChangeDateFrom = (date) => {
        setSelectedDateFrom(date);
    };

    const [selectedDateTo, setSelectedDateTo] = React.useState(new Date());
    const handleChangeDateTo = (date) => {
        setSelectedDateTo(date);
    };

    const [selectedWebPage, setSelectedWebPage] = React.useState();
    const handleSetSelectedWebPage = (event, newValue, reason, details) => {
        setSelectedWebPage(newValue);
    }

    const [selectedLanguage, setSelectedLanguage] = React.useState();
    const handleSetSelectedLanguage = (event, newValue, reason, details) => {
        setSelectedLanguage(newValue);
    }

    const [selectedCountry, setSelectedCountry] = React.useState();
    const handleSetSelectedCountry = (event, newValue, reason, details) => {
        setSelectedCountry(newValue);
    }

    const [selectedPhrase, setSelectedPhrase] = React.useState();
    const handleSetSelectedPhrase = (event) => {
        setSelectedPhrase(event.target.value);
    }

    const onResetClicked = (event) => {

        setSelectedDateFrom(aWeekAgo);
        setSelectedDateTo(new Date());
        setSelectedWebPage("");
        setSelectedCountry("");
        setSelectedCountry("");
        setSelectedPhrase("");
        
    };
    
    const onSearchClicked = (event) => {

        var searchData = {
            dateFrom: selectedDateFrom,
            dateTo: selectedDateTo,
            webPage: selectedWebPage,
            language: selectedLanguage,
            country: selectedCountry,
            phrase: selectedPhrase
        }

        var jsonData = JSON.stringify(searchData);

        alert("search:\n" + jsonData);
    };

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
                            onChange={handleChangeDateFrom}
                            value={selectedDateFrom}
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
                            onChange={handleChangeDateTo}
                            value={selectedDateTo}
                            KeyboardButtonProps={{
                                'aria-label': 'change date',
                            }}
                        />

{/* TODO: https://material-ui.com/components/autocomplete/#asynchronous-requests */}

                        <Autocomplete
                            id="web-page"
                            options={webPages}
                            style={{ width: 300 }}
                            openOnFocus
                            inputValue={selectedWebPage}
                            onInputChange={handleSetSelectedWebPage}
                            renderInput={(params) => 
                                <TextField
                                    {...params}
                                    label="Web page" margin="normal" />}
                        />

                        <Autocomplete
                            id="language"
                            options={languages}
                            style={{ width: 300 }}
                            openOnFocus
                            onInputChange={handleSetSelectedLanguage}
                            inputValue={selectedLanguage}
                            renderInput={(params) => 
                                <TextField 
                                    {...params} 
                                    label="Language" margin="normal" />}
                        />

                        <Autocomplete
                            id="country"
                            options={countries}
                            style={{ width: 300 }}
                            openOnFocus
                            onInputChange={handleSetSelectedCountry}
                            inputValue={selectedCountry}
                            renderInput={(params) => 
                                <TextField 
                                    {...params} 
                                    label="Country" margin="normal" />}
                        />

                        <TextField
                            id="any-phrase"
                            label="Any phrase"
                            margin="normal"
                            onChange={handleSetSelectedPhrase}
                            value={selectedPhrase}
                        />

                    </Grid>
                </MuiPickersUtilsProvider>

                <Grid
                    style={{ display: 'flex', justifyContent: 'flex-end' }}
                    justify="space-around"
                >

                    <Button
                        variant="contained"
                        className="button-submit"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }}
                        onClick={(event) => onResetClicked(event)}>
                        Reset
                        </Button>

                    <Button
                        variant="contained"
                        className="button-submit"
                        color="primary"
                        primary={true}
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }}
                        onClick={(event) => onSearchClicked(event)}
                    >
                        Search
                    </Button>

                </Grid>
            </Box>
        </form>
    );
}