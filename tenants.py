from flask import Blueprint, g, render_template, redirect, url_for
from database import Users, session as sess, Tenants, Property

tenants_bp = Blueprint('tenants', __name__)

if __name__ == '__main__':
    pass