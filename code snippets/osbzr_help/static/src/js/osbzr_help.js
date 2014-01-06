
openerp.osbzr_help = function(session) {

session.web.ViewManagerAction.include({
    start: function() {
        var self = this;
        self.$el.find('a.osbzr_model_help').click(self.on_click_help_link);
        return this._super.apply(this, arguments);
    },
    on_click_help_link: function(e) {
        e.preventDefault();
        window.open('http://www.osbzr.com/help.php?page='+this.dataset.model);
    },
});

};

