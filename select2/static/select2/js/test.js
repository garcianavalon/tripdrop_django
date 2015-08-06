$(function(){
    $('select').each(function(){
        // if there is a variable with the options, initialize the select2 element
        if (typeof window['select2_' + this.id] !== 'undefined') {
            $('#' + this.id).select2(window['select2_' + this.id]);
        }
    });
})