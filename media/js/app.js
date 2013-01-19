// vim: set foldmethod=marker :
/**
 * @dependency Underscore.js v1.4.3 <http://underscorejs.org/>
 *             jQuery v1.9.0 <http://jquery.com/>
 */
var $d, $a;

$a = {};

$a.consoleLog = function(){
    if ('console' in this && 'log' in this.console) {
        try {
            return this.console.log.apply(this.console, arguments);
        } catch (err) {// For IE
            var args = Array.prototype.slice.apply(arguments);
            return this.console.log(args.join(' '));
        }
    }
}

$d = $a.consoleLog;

$a.attachConfirmation = function(htmlId, text){
  $('#' + htmlId).click(function(){
    return confirm(text);
  });
}
