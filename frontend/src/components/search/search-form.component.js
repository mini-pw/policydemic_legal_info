import React, { useEffect, useCallback } from 'react';
import 'date-fns';
import { useForm } from "react-hook-form";

import Grid from '@material-ui/core/Grid';
import TextField from '@material-ui/core/TextField';
import Autocomplete from '@material-ui/lab/Autocomplete';
import Box from '@material-ui/core/Box';

import { KeyboardDatePicker, MuiPickersUtilsProvider } from '@material-ui/pickers';
import DateFnsUtils from '@date-io/date-fns';
import Button from '@material-ui/core/Button';
import Typography from '@material-ui/core/Typography';
import AsyncAutocomplete from '../form/async-autocomplete.component';

export default function SearchFormComponent({ type, onSearch, onReset }) {

    const aWeekAgo = new Date(new Date().getTime() - 7 * 24 * 60 * 60 * 1000)

    const [selectedDateFrom, setSelectedDateFrom] = React.useState(aWeekAgo);
    const handleChangeDateFrom = (date) => {
        setSelectedDateFrom(date);
        setValue("dateTo", date.toISOString());
    };

    const [selectedDateTo, setSelectedDateTo] = React.useState(new Date());
    const handleChangeDateTo = (date) => {
        setSelectedDateTo(date);
        setValue("dateFrom", date.toISOString());
    };

    const onResetClicked = (event) => {

        setSelectedDateFrom(aWeekAgo);
        setSelectedDateTo(new Date());
        
        // setValue("web-page", []);
        // setValue("language", []);
        // setValue("country", []);
        // setValue("any-phrase", "");

        document.getElementById("search-form").reset();

        onReset();
    };

    const onSubmit = useCallback(data => {
        console.log(data);

        onSearch(data);

    }, [type])

    const { register, handleSubmit, setValue } = useForm();

    return (
        <form id="search-form" onSubmit={handleSubmit(onSubmit)}>
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

                        <AsyncAutocomplete
                            name="web-pages"
                            collectionName="webpages"
                            style={{ width: 300 }}
                            openOnFocus
                            fullWidth
                            multiple
                            renderInput={(params) =>
                                <TextField
                                    {...params}
                                    label="Web page" margin="normal" />}
                            onChange={(_, opts) => setValue("web-page", opts.map(o => o.value).join(','))}
                        />

                        <AsyncAutocomplete
                            name="languages"
                            collectionName="languages"
                            style={{ width: 300 }}
                            openOnFocus
                            fullWidth
                            multiple
                            renderInput={(params) =>
                                <TextField
                                    {...params}
                                    label="Language" margin="normal" />}
                            onChange={(_, opts) => setValue("language", opts.map(o => o.value).join(','))}
                        />

                        <AsyncAutocomplete
                            name="country"
                            collectionName="countries"
                            style={{ width: 300 }}
                            openOnFocus
                            fullWidth
                            multiple
                            renderInput={(params) =>
                                <TextField
                                    {...params}
                                    label="Country" margin="normal" />}
                            onChange={(_, opts) => setValue("country", opts.map(o => o.value).join(','))}
                        />

                        <TextField
                            name="any-phrase"
                            label="Any phrase"
                            margin="normal"
                            onChange={(event) => setValue("any-phrase", event.value)}
                        />

                    </Grid>
                </MuiPickersUtilsProvider>

                <Grid
                    container
                    style={{ display: 'flex', justifyContent: 'flex-end' }}
                    justify="space-around"
                >

                    <Button
                        variant="contained"
                        className="button-submit"
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }}
                        onClick={(event) => onResetClicked(event)}>
                        Reset
                    </Button>

                    <Button
                        variant="contained"
                        className="button-submit"
                        color="primary"
                        type="submit"
                        style={{ position: 'relative', right: 5, top: 5, margin: 5 }}
                        form="search-form" 
                    >
                        Search
                    </Button>

                </Grid>
            </Box>
        </form>
    );
}